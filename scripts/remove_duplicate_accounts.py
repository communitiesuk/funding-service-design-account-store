#!/usr/bin/env python3
"""Script to remove duplicated email accounts from the account store and update
account ids in application store, assessment store with the new unique account id"""
import os
from uuid import uuid4

import psycopg2

ACCOUNT_STORE_DB = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/account_store",
)
APPLICATION_STORE_DB = os.getenv(
    "APPLICATION_STORE_DB_URL",
    "postgresql://postgres:password@localhost:5432/application_store",
)
ASSESSMENT_STORE_DB = os.getenv(
    "ASSESSMENT_STORE_DB_URL",
    "postgresql://postgres:password@localhost:5432/assessment_store",
)


def find_duplicate_emails(connection_string):
    """
    Returns data in the below format if duplicated emails are found in the db

    duplicate_emails_dict = {
        "test.example@google.com": [
            {
                "email": "test.example@test.com",
                "id": "428cf967-f5d5-4a5d-9e6d-7d33cee93be6",
                "full_name": "Tester Home",
                "azure_ad_subject_id": None,
                "roles": [],
            },
            {
                "email": "Test.Example@test.com",
                "id": "13636293-8a80-452d-a3f6-be1f29a5c0f4",
                "full_name": None,
                "azure_ad_subject_id": "967-f5d5-4a5d-9e6d-7d33ce",
                "roles": [
                    {
                        "id": "01d837aa-83d5-49b8-90b9-82662e6c9a40",
                        "role": "COF_ENGLAND",
                    },
                    {
                        "id": "13636293-8a80-452d-a3f6-be1f29a5c0f4",
                        "role": "COF_LEAD_ASSESSOR",
                    },
                ],
            },
        ]
    }
    """

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        query = """
            SELECT LOWER(email) AS email, COUNT(*) AS count
            FROM account
            GROUP BY LOWER(email)
            HAVING COUNT(*) > 1;
        """

        cursor.execute(query)
        results = cursor.fetchall()
        duplicate_emails_dict = {}

        # Convert the results to a list
        duplicate_emails = [result[0] for result in results]

        if duplicate_emails:
            query = """
                SELECT email, id, full_name, azure_ad_subject_id
                FROM account
                WHERE email ILIKE '%{email}%';
            """

            for email_data in duplicate_emails:
                cursor.execute(query.format(email=email_data))
                results = cursor.fetchall()
                duplicate_emails_dict[email_data] = [
                    {
                        "email": item[0],
                        "id": item[1],
                        "full_name": item[2],
                        "azure_ad_subject_id": item[3],
                    }
                    for item in results
                ]

            query = """
                SELECT id, role
                FROM role
                WHERE account_id='{account_id}';
            """

            for data in duplicate_emails_dict.values():
                for item in data:
                    cursor.execute(query.format(account_id=item["id"]))
                    results = cursor.fetchall()
                    item["roles"] = [
                        {"id": role[0], "role": role[1]} for role in results
                    ]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return duplicate_emails_dict

    except Exception as e:
        print("Error:", e)
        return None


def cascade_columns_data(duplicate_emails):
    """
    Return data in the below format

    new_accounts_dict = {
        "test.example@google.com": {
            "id": "23636293-8a80-452d-a3f6-be1f29a5c0f4",
            "full_name": "Tester Home",
            "azure_ad_subject_id": "967-f5d5-4a5d-9e6d-7d33ce",
            "roles": ["COF_ENGLAND", "COF_LEAD_ASSESSOR"],
        }
    }
    """
    new_accounts_dict = {}
    for email, data in duplicate_emails.items():
        full_name = ""
        azure_ad_subject_id = ""
        roles = []
        for item in data:
            full_name = item["full_name"] if item["full_name"] else full_name
            azure_ad_subject_id = (
                item["azure_ad_subject_id"]
                if item["azure_ad_subject_id"]
                else azure_ad_subject_id
            )
            for role in item["roles"]:
                if role["role"] not in roles:
                    roles.append(role["role"])
        new_accounts_dict[email] = {
            "id": str(uuid4()),
            "full_name": full_name,
            "azure_ad_subject_id": azure_ad_subject_id,
            "roles": roles,
        }

    return new_accounts_dict


def remove_and_update_duplicate_accounts(
    duplicate_emails, new_accounts_dict, account_store_db_string
):
    """
    Return data in the below format

    account_id_dict = {
        "test.example@google.com": {
            "new_id": "23636293-8a80-452d-a3f6-be1f29a5c0f4",
            "old_id_list": ['428cf967-f5d5-4a5d-9e6d-7d33cee93be6','13636293-8a80-452d-a3f6-be1f29a5c0f4'],
        }
    }
    """
    # There is 1-to-many relationship between account & roles tables.
    # So first remove the records from role table and then in the accounts table
    if duplicate_emails:
        try:
            conn = psycopg2.connect(account_store_db_string)
            cursor = conn.cursor()

            # SQL statement for bulk delete of roles
            print("Removing the roles associated with duplicated email accounts...")
            delete_query = "DELETE FROM role WHERE id IN ({id_list})"
            data_to_delete_roles = [
                f"'{role['id']}'"
                for value in duplicate_emails.values()
                for data in value
                for role in data["roles"]
            ]
            cursor.execute(delete_query.format(id_list=",".join(data_to_delete_roles)))
            print(f"Successfully removed the roles ids {data_to_delete_roles}")

            # SQL statement for bulk delete of account
            print("Removing the duplicated email accounts from accounts table....")
            delete_query = "DELETE FROM account WHERE id IN ({id_list})"
            data_to_delete_accounts = [
                f"'{data['id']}'"
                for value in duplicate_emails.values()
                for data in value
            ]
            cursor.execute(
                delete_query.format(id_list=",".join(data_to_delete_accounts))
            )
            print(f"Successfully removed the account ids {data_to_delete_accounts}")

            # SQL statement for bulk INSERT of unique accounts
            print("Inserting the unique email accounts in accounts table....")
            insert_query = (
                "INSERT INTO account (id, email, full_name, azure_ad_subject_id) VALUES"
                " (%s, %s, %s, %s)"
            )
            data_to_insert_in_account_table = [
                (
                    data["id"],
                    email,
                    data["full_name"],
                    data["azure_ad_subject_id"],
                )
                for email, data in new_accounts_dict.items()
            ]
            cursor.executemany(insert_query, data_to_insert_in_account_table)
            print(
                "Successfully inserted the account ids"
                f" {data_to_insert_in_account_table}"
            )

            # SQL statement for bulk INSERT of roles for accounts
            print("Inserting the roles associated with the accounts in role table....")
            insert_query = "INSERT INTO role (id, account_id, role) VALUES (%s, %s, %s)"
            data_to_insert_in_role_table = [
                (str(uuid4()), data["id"], role)
                for data in new_accounts_dict.values()
                for role in data["roles"]
            ]
            cursor.executemany(insert_query, data_to_insert_in_role_table)
            print(f"Successfully inserted the roles ids {data_to_insert_in_role_table}")

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # return account_id_dict with new & old account id's
            account_id_dict = {}
            for email, data in duplicate_emails.items():
                account_id_dict[email] = {
                    "new_id": new_accounts_dict[email]["id"],
                    "old_id_list": [f"'{item['id']}'" for item in data],
                }

            return account_id_dict

        except Exception as e:
            print("Error:", e)
            return None


def update_user_id_in_other_db(
    account_id_dict: dict,
    application_store_db_string,
    assessment_store_db_string,
):
    if account_id_dict:
        # update user ids in application store
        try:
            conn = psycopg2.connect(application_store_db_string)
            cursor = conn.cursor()

            # update accound_id's in the application store db
            update_query = (
                "UPDATE applications SET account_id = '{new_id}' WHERE account_id IN"
                " ({old_id_list})"
            )

            for email, data in account_id_dict.items():
                print(
                    f"updating account_ids {data['old_id_list']} with"
                    f" {data['new_id']} in applications table & for the account {email}"
                )
                cursor.execute(
                    update_query.format(
                        new_id=data["new_id"],
                        old_id_list=",".join(data["old_id_list"]),
                    )
                )

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except Exception as e:
            print("Error:", e)

        # update user ids in assessment store
        try:
            conn = psycopg2.connect(assessment_store_db_string)
            cursor = conn.cursor()

            # update user_id's in the comments, scores and flag_update tables from assessment store db
            update_query_comments = (
                "UPDATE comments SET user_id = '{new_id}' WHERE user_id IN"
                " ({old_id_list})"
            )
            update_query_scores = (
                "UPDATE scores SET user_id = '{new_id}' WHERE user_id IN"
                " ({old_id_list})"
            )
            update_query_flag_updates = (
                "UPDATE flag_update SET user_id = '{new_id}' WHERE user_id IN"
                " ({old_id_list})"
            )
            update_query_qa_complete = (
                "UPDATE qa_complete SET user_id = '{new_id}' WHERE user_id IN"
                " ({old_id_list})"
            )

            for email, data in account_id_dict.items():
                new_id = data["new_id"]
                old_id_list = ",".join(data["old_id_list"])

                print(
                    f"updating user_ids [{old_id_list}] with {new_id} in comments,"
                    " scores, flag_update and qa_complete tables for the account"
                    f" {email} "
                )
                cursor.execute(
                    update_query_comments.format(
                        new_id=new_id,
                        old_id_list=old_id_list,
                    )
                )
                cursor.execute(
                    update_query_scores.format(
                        new_id=new_id,
                        old_id_list=old_id_list,
                    )
                )
                cursor.execute(
                    update_query_flag_updates.format(
                        new_id=new_id,
                        old_id_list=old_id_list,
                    )
                )
                cursor.execute(
                    update_query_qa_complete.format(
                        new_id=new_id,
                        old_id_list=old_id_list,
                    )
                )

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    duplicate_emails = find_duplicate_emails(ACCOUNT_STORE_DB)

    # # Uncomment below lines to dump `duplicate_emails` to excel file
    # import pandas as pd
    # dict_data=[]
    # for email, data in duplicate_emails.items():
    #     for item in data:
    #         dict_data.append(item)
    # df = pd.DataFrame(data=dict_data)
    # df.to_excel('dict1.xlsx')

    new_accounts_dict = cascade_columns_data(duplicate_emails)
    account_id_dict = remove_and_update_duplicate_accounts(
        duplicate_emails, new_accounts_dict, ACCOUNT_STORE_DB
    )
    update_user_id_in_other_db(
        account_id_dict, APPLICATION_STORE_DB, ASSESSMENT_STORE_DB
    )

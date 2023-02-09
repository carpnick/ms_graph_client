from ms_graph_client import GraphAPI, GraphAPIConfig, GraphCacheAPI, Generator
from ms_graph_client.services.groups import Groups
import time
import datetime


class IntegrationTests:
    @staticmethod
    def run_tests(config: GraphAPIConfig) -> None:

        automation_app_name2 = "Test"

        # If these values change - we need to do an action
        # Group name will be the primary identifier - that will net a create
        # If update not supported - it will create another one and delete existing -
        # delete before create will make this work
        aws_app_name = "AWS IAM Identity Center (successor to AWS Single Sign-On)"
        group_name = "NickTest"

        graph_api_wrapper = GraphAPI(config=config)

        # Owners
        IntegrationTests.add_owner_remove_owner_list_owner(api_wrapper=graph_api_wrapper)

        # Add/remove members from groups
        IntegrationTests.add_remove_list_members_to_group(api_wrapper=graph_api_wrapper)

        # Create/update/delete Groups
        IntegrationTests.create_update_delete_group(
            api_wrapper=graph_api_wrapper, automation_app_name=automation_app_name2, group_name=group_name
        )

        # Associate group to App (And disassociate)
        IntegrationTests.assign_unassign_group_to_app(
            api_wrapper=graph_api_wrapper,
            app_name=aws_app_name,
            automation_app_name=automation_app_name2,
            group_name=group_name,
        )

        # Create 2000 groups
        # Only enable if you are in a test environment
        # IntegrationTests.limit_testing_for_groups(automation_app_name=automation_app_name,
        #                                           api_wrapper=graph_api_wrapper,
        #                                           aws_app_name=aws_app_name)

    @staticmethod
    def create_update_delete_group(
        api_wrapper: GraphAPI,
        automation_app_name: str,
        group_name: str,
    ) -> None:
        print("Creating Group")

        # Find app owner based on my automation application service prinicpal
        owner_app_id = api_wrapper.applications.get_by_application_name(app_name=automation_app_name)["appId"]
        owner_sp_id = api_wrapper.applications.get_service_principal_by_app_id(owner_app_id)["id"]
        owner_url = Generator(api_wrapper.groups.config).service_principal_url(app_service_principal_id=owner_sp_id)

        # Create
        group_id = api_wrapper.groups.create(
            group_name=group_name,
            group_description="123",
            owners=[owner_url],
            group_type=Groups.GroupType.SECURITY,
            with_stabilization=True,
        )

        print("Updating Group")
        api_wrapper.groups.update(group_id=group_id, group_name=group_name + "123")

        print("Deleting Group")
        api_wrapper.groups.delete(group_id=group_id, group_name=group_name, with_stabilization=True)

    @staticmethod
    def assign_unassign_group_to_app(
        api_wrapper: GraphAPI,
        app_name: str,
        automation_app_name: str,
        group_name: str,
    ) -> None:
        print("Creating Group")
        owner_app_id = api_wrapper.applications.get_by_application_name(app_name=automation_app_name)["appId"]
        owner_sp_id = api_wrapper.applications.get_service_principal_by_app_id(owner_app_id)["id"]
        owner_url = Generator(api_wrapper.groups.config).service_principal_url(app_service_principal_id=owner_sp_id)

        # Create
        group_id = api_wrapper.groups.create(
            group_name=group_name,
            owners=[owner_url],
            group_type=Groups.GroupType.SECURITY,
            with_stabilization=True,
            group_description="123",
        )

        print("Assigning Group")
        json_output = api_wrapper.applications.assign_group_to_app(
            app_name=app_name, group_id=group_id, with_stabilization=True
        )
        assign_add_id = json_output["id"]

        print("Unassigning Group")
        api_wrapper.applications.unassign_group_to_app(
            app_name=app_name, assigned_to_id=assign_add_id, group_id=group_id, with_stabilization=True
        )

        print("Deleting Group")
        api_wrapper.groups.delete(group_id, with_stabilization=True, group_name=group_name)

    @staticmethod
    def add_owner_remove_owner_list_owner(api_wrapper: GraphAPI) -> None:
        print("Getting Group Info")
        group_info = api_wrapper.groups.get_by_name(group_name="TestGroup123")
        print("Getting Group Owners")
        owners = api_wrapper.groups.list_owners(group_id=group_info["id"])
        for it in owners:
            print("Removing Group Owner: " + str(it))
            api_wrapper.groups.remove_owner(group_id=group_info["id"], user_obj_id=it["id"])

        print("Waiting for owners to be 0")
        while True:
            time.sleep(5)
            s = api_wrapper.groups.list_owners(group_id=group_info["id"])
            if len(s) == 0:
                time.sleep(3)
                break
        print("Owners are 0")

        owners = []
        owners.append(api_wrapper.users.get_user(upn="AdeleV@qkdw.onmicrosoft.com")["id"])
        owners.append(api_wrapper.users.get_user(upn="carpnick2@qkdw.onmicrosoft.com")["id"])

        for item in owners:
            print("Adding Group Owner: " + str(item))
            api_wrapper.groups.add_owner(group_id=group_info["id"], user_obj_id=item)

    @staticmethod
    def add_remove_list_members_to_group(api_wrapper: GraphAPI) -> None:
        # List members
        group_info = api_wrapper.groups.get_by_name(group_name="TestGroup123")
        members = api_wrapper.groups.list_group_members(group_id=group_info["id"])  # noqa: F841

        # Add a member
        user_obj = api_wrapper.users.get_user(upn="carpnick2@qkdw.onmicrosoft.com")
        print("Adding Nick to group")
        api_wrapper.groups.add_member(group_id=group_info["id"], object_id=user_obj["id"], with_stabilization=True)

        # Remove a member
        members2 = api_wrapper.groups.list_group_members(group_id=group_info["id"])
        for member in members2:
            if member["userPrincipalName"] == "carpnick2@qkdw.onmicrosoft.com":
                print("Removing Nick from group")
                api_wrapper.groups.remove_member(
                    group_id=group_info["id"], object_id=member["id"], with_stabilization=True
                )

        # Add more than one member

        user_obj1 = api_wrapper.users.get_user(upn="carpnick2@qkdw.onmicrosoft.com")
        user_obj2 = api_wrapper.users.get_user(upn="nicktestuser@qkdw.onmicrosoft.com")

        print("Adding Nick and nick test user to group")

        api_wrapper.groups.add_members(group_id=group_info["id"], object_ids=[user_obj1["id"], user_obj2["id"]])
        print("Sleeping 25 seconds")
        time.sleep(25)
        print("Removing Nick and nick test user from group")
        api_wrapper.groups.remove_member(group_id=group_info["id"], object_id=user_obj1["id"], with_stabilization=False)
        api_wrapper.groups.remove_member(group_id=group_info["id"], object_id=user_obj2["id"], with_stabilization=False)

    @staticmethod
    def limit_testing_for_groups(
        automation_app_name: str,
        aws_app_name: str,
        group_name: str,
        api_wrapper: GraphAPI,
    ) -> None:
        # Make sure we can create over 1000 groups with this design....

        # Add 1000 groups then delete them
        total_groups = 2000

        # Automation app Service principal id
        owner_app_id = api_wrapper.applications.get_by_application_name(app_name=automation_app_name)["appId"]
        owner_sp_id = api_wrapper.applications.get_service_principal_by_app_id(owner_app_id)["id"]
        owner_url = Generator(api_wrapper.groups.config).service_principal_url(app_service_principal_id=owner_sp_id)

        my_group_ids = []
        for i in range(0, total_groups):
            print(datetime.datetime.now().isoformat() + " - Creating group: " + str(i))
            gid = api_wrapper.groups.create(
                group_name=group_name + str(i),
                group_type=Groups.GroupType.SECURITY,
                owners=[owner_url],
                with_stabilization=False,
                group_description="123",
            )
            my_group_ids.append(gid)

        for xyz in my_group_ids:
            print(datetime.datetime.now().isoformat() + " - Assigning group: " + str(xyz))
            api_wrapper.applications.assign_group_to_app(app_name=aws_app_name, group_id=xyz, with_stabilization=False)

        for x in my_group_ids:
            print(datetime.datetime.now().isoformat() + " - Deleting group: " + str(x))
            api_wrapper.groups.delete(group_id=x, with_stabilization=False, group_name="")


class Helpers:
    @staticmethod
    def delete_sso_groups() -> None:
        import boto3  # type: ignore

        # Deletion of all SSO Groups manually
        # import boto3
        identity_store_id = "xxxxxxxx"
        iclient = boto3.client(
            service_name="identitystore",
            aws_access_key_id="xxxxxxx",
            aws_secret_access_key="xxxxxxx",
            region_name="us-east-1",
        )

        paginator = iclient.get_paginator("list_groups")
        group_ids = []

        for page in paginator.paginate(IdentityStoreId=identity_store_id):
            for group in page["Groups"]:
                group_ids.append(group["GroupId"])

        for group_id in group_ids:
            print("deleting group: " + group_id)
            iclient.delete_group(IdentityStoreId=identity_store_id, GroupId=group_id)

    @staticmethod
    def deleting_azure_groups_named_nicktest_up_to_2000(graph_api_wrapper: GraphAPI) -> None:
        for i in range(0, 2000):
            group_name = "NickTest" + str(i)
            print("Deleting: " + group_name)

            if graph_api_wrapper.groups.exists_by_name(group_name=group_name):
                gid = graph_api_wrapper.groups.get_by_name(group_name=group_name)["id"]
                graph_api_wrapper.groups.delete(group_id=gid, group_name=group_name, with_stabilization=False)
            else:
                print("Group doesnt exist: " + group_name)


if __name__ == "__main__":
    # If any 4 of these change - ignore update call
    client_id = "xxxxxxxx"
    tenant_id = "xxxxxxxx"
    client_secret = "xxxxxxxx"


    graphapi_config = GraphAPIConfig(
        client_id=client_id,
        tenant_id=tenant_id,
        client_secret=client_secret,
        api_url="https://graph.microsoft.com/v1.0",
    )

    IntegrationTests.run_tests(graphapi_config)

    cache_reading = GraphCacheAPI(config=graphapi_config)
    user = cache_reading.users.get_user("carpnick2@qkdw.onmicrosoft.com")
    user2 = cache_reading.users.get_user("carpnick2@qkdw.onmicrosoft.com")
    print()

"""Stream type classes for tap-hubspot."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_hubspot.client import DynamicHubspotStream, DynamicIncrementalHubspotStream, HubspotStream
from typing import Optional, Any, Dict

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


class ContactStream(DynamicIncrementalHubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/contacts
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "contacts"
    path = "/objects/contacts"
    incremental_path = "/objects/contacts/search"
    primary_keys = ["id"]
    replication_key = "lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class UsersStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/settings/user-provisioning
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = id keys for replication
    records_jsonpath = json response body
    """

    name = "users"
    path = "/users"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property("email", StringType),
        Property("roleIds", ArrayType(StringType)),
        Property("primaryteamid", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """

        return "https://api.hubapi.com/settings/v3"


class OwnersStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/owners#endpoint?spec=GET-/crm/v3/owners/
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "owners"
    path = "/owners"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.
    partitions = [{"archived": True}, {"archived": False}]

    schema = PropertiesList(
        Property("id", StringType),
        Property("email", StringType),
        Property("firstName", StringType),
        Property("lastName", StringType),
        Property("userId", IntegerType),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["archived"] = context["archived"]
        return params

class TicketPipelineStream(HubspotStream):

    """
    https://legacydocs.hubspot.com/docs/methods/tickets/get-all-tickets
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "ticket_pipelines"
    path = "/pipelines/tickets"
    primary_keys = ["createdAt"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("label", StringType),
        Property("displayOrder", IntegerType),
        Property("active", BooleanType),
        Property(
            "stages",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("displayOrder", IntegerType),
                    Property(
                        "metadata",
                        ObjectType(
                            Property("ticketState", StringType),
                            Property("isClosed", StringType),
                        ),
                    ),
                    Property("stageId", StringType),
                    Property("createdAt", IntegerType),
                    Property("updatedAt", StringType),
                    Property("active", BooleanType),
                ),
            ),
        ),
        Property("objectType", StringType),
        Property("objectTypeId", StringType),
        Property("pipelineId", StringType),
        Property("createdAt", IntegerType),
        Property("updatedAt", StringType),
        Property("default", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm-pipelines/v1"


class DealPipelineStream(HubspotStream):

    """
    https://legacydocs.hubspot.com/docs/methods/deals/get-all-deals
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "deal_pipelines"
    path = "/pipelines/deals"
    primary_keys = ["createdAt"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("label", StringType),
        Property("displayOrder", IntegerType),
        Property("active", BooleanType),
        Property(
            "stages",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("displayOrder", IntegerType),
                    Property(
                        "metadata",
                        ObjectType(
                            Property("isClosed", BooleanType),
                            Property("probability", StringType),
                        ),
                    ),
                    Property("stageId", StringType),
                    Property("createdAt", IntegerType),
                    Property("updatedAt", IntegerType),
                    Property("active", BooleanType),
                ),
            ),
        ),
        Property("objectType", StringType),
        Property("objectTypeId", StringType),
        Property("pipelineId", StringType),
        Property("createdAt", IntegerType),
        Property("updatedAt", IntegerType),
        Property("default", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm-pipelines/v1"


class EmailSubscriptionStream(HubspotStream):

    """
    https://legacydocs.hubspot.com/docs/methods/email/get_subscriptions
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = id keys for replication
    records_jsonpath = json response body
    """

    name = "email_subscriptions"
    path = "/subscriptions"
    primary_keys = ["id"]
    records_jsonpath = "$[subscriptionDefinitions][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("portalId", IntegerType),
        Property("name", StringType),
        Property("description", StringType),
        Property("active", BooleanType),
        Property("internal", BooleanType),
        Property("category", StringType),
        Property("channel", StringType),
        Property("internalName", StringType),
        Property("businessUnitId", IntegerType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/email/public/v1"


class PropertyTicketStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_tickets"
    path = "/properties/tickets"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyDealStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_deals"
    path = "/properties/deals"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
        Property("calculationFormula", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyContactStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_contacts"
    path = "/properties/contacts"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCompanyStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_companies"
    path = "/properties/company"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyProductStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_products"
    path = "/properties/product"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyLineItemStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_line_items"
    path = "/properties/line_item"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyEmailStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_emails"
    path = "/properties/email"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyPostalMailStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_postal_mails"
    path = "/properties/postal_mail"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCallStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_calls"
    path = "/properties/call"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyMeetingStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_meetings"
    path = "/properties/meeting"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyTaskStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_tasks"
    path = "/properties/task"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCommunicationStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_communications"
    path = "/properties/communication"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyNotesStream(HubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "properties"
    path = "/properties/notes"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("updatedAt", StringType),
        Property("createdAt", StringType),
        Property("name", StringType),
        Property("label", StringType),
        Property("type", StringType),
        Property("fieldType", StringType),
        Property("description", StringType),
        Property("groupName", StringType),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property("label", StringType),
                    Property("description", StringType),
                    Property("value", StringType),
                    Property("displayOrder", IntegerType),
                    Property("hidden", BooleanType),
                ),
            ),
        ),
        Property("displayOrder", IntegerType),
        Property("calculated", BooleanType),
        Property("externalOptions", BooleanType),
        Property("hasUniqueValue", BooleanType),
        Property("hidden", BooleanType),
        Property("hubspotDefined", BooleanType),
        Property(
            "modificationMetadata",
            ObjectType(
                Property("readOnlyOptions", BooleanType),
                Property("readOnlyValue", BooleanType),
                Property("readOnlyDefinition", BooleanType),
                Property("archivable", BooleanType),
            ),
        ),
        Property("formField", BooleanType),
        Property("hubspot_object", StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        Merges all the property stream data into a single property table
        """

        property_ticket = PropertyTicketStream(self._tap, schema={"properties": {}})
        property_deal = PropertyDealStream(self._tap, schema={"properties": {}})
        property_contact = PropertyContactStream(self._tap, schema={"properties": {}})
        property_company = PropertyCompanyStream(self._tap, schema={"properties": {}})
        property_product = PropertyProductStream(self._tap, schema={"properties": {}})
        property_lineitem = PropertyLineItemStream(self._tap, schema={"properties": {}})
        property_email = PropertyEmailStream(self._tap, schema={"properties": {}})
        property_postalmail = PropertyPostalMailStream(
            self._tap, schema={"properties": {}}
        )
        property_call = PropertyCallStream(self._tap, schema={"properties": {}})
        property_meeting = PropertyMeetingStream(self._tap, schema={"properties": {}})
        property_task = PropertyTaskStream(self._tap, schema={"properties": {}})
        property_communication = PropertyCommunicationStream(
            self._tap, schema={"properties": {}}
        )
        property_records = (
            list(property_ticket.get_records(context))
            + list(property_deal.get_records(context))
            + list(property_contact.get_records(context))
            + list(property_company.get_records(context))
            + list(property_product.get_records(context))
            + list(property_lineitem.get_records(context))
            + list(property_email.get_records(context))
            + list(property_postalmail.get_records(context))
            + list(property_call.get_records(context))
            + list(property_meeting.get_records(context))
            + list(property_task.get_records(context))
            + list(property_communication.get_records(context))
            + list(super().get_records(context))
        )

        return property_records


class CompanyStream(DynamicIncrementalHubspotStream):

    """
    https://developers.hubspot.com/docs/api/crm/companies
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "companies"
    path = "/objects/companies"
    incremental_path = "/objects/companies/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class DealStream(DynamicHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/deals
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "deals"
    path = "/objects/deals"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.
    partitions = [{"archived": True}, {"archived": False}]

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["archived"] = context["archived"]
        params["associations"] = "companies,line_item"  # get associated companies
        return params


class FeedbackSubmissionsStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/feedback-submissions
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "feedback_submissions"
    path = "/objects/feedback_submissions"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("city", StringType),
                Property("createdDate", StringType),
                Property("domain", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("industry", StringType),
                Property("name", StringType),
                Property("phone", StringType),
                Property("state", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class LineItemStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/line-items
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "line_items"
    path = "/objects/line_items"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_product_id", StringType),
                Property("hs_recurring_billing_period", StringType),
                Property("name", StringType),
                Property("price", StringType),
                Property("quantity", StringType),
                Property("recurringbillingfrequency", StringType),
                Property("amount", StringType),
                Property("start_date", StringType),
                Property("estimated_end_date", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
    
    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)

        required_properties = [
            "createdate",
            "hs_lastmodifieddate",
            "hs_product_id",
            "hs_recurring_billing_period",
            "name",
            "price",
            "quantity",
            "recurringbillingfrequency",
            "amount",
            "start_date",
            "estimated_end_date",
        ]
        params["properties"] = ",".join(required_properties)

        return params


class ProductStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/products
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "products"
    path = "/objects/products"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("description", StringType),
                Property("hs_cost_of_goods_sold", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_recurring_billing_period", StringType),
                Property("hs_sku", StringType),
                Property("name", StringType),
                Property("price", StringType),
                Property("hs_folder", StringType),
                Property("hs_price_czk", StringType),
                Property("hs_price_eur", StringType),
                Property("hs_price_usd", StringType),
                Property("hs_product_type", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
    
    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)

        required_properties = [
            "createdate",
            "description",
            "hs_lastmodifieddate",
            "hs_product_id",
            "hs_recurring_billing_period",
            "name",
            "price",
            "hs_folder",
            "hs_price_czk",
            "hs_price_eur",
            "hs_price_usd",
            "hs_product_type",
        ]
        params["properties"] = ",".join(required_properties)

        return params


class TicketStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/tickets
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "tickets"
    path = "/objects/tickets"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_pipeline", StringType),
                Property("hs_pipeline_stage", StringType),
                Property("hs_ticket_priority", StringType),
                Property("hubspot_owner_id", StringType),
                Property("subject", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class QuoteStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/quotes
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "quotes"
    path = "/objects/quotes"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("hs_createdate", StringType),
                Property("hs_expiration_date", StringType),
                Property("hs_quote_amount", StringType),
                Property("hs_quote_number", StringType),
                Property("hs_status", StringType),
                Property("hs_terms", StringType),
                Property("hs_title", StringType),
                Property("hubspot_owner_id", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class GoalStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/goals
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "goals"
    path = "/objects/goal_targets"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("hs_created_by_user_id", StringType),
                Property("hs_end_datetime", StringType),
                Property("hs_goal_name", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_start_datetime", StringType),
                Property("hs_target_amount", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class CallStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/calls
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "calls"
    path = "/objects/calls"
    incremental_path = "/objects/calls/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class CommunicationStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/communications
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "communications"
    path = "/objects/communications"
    incremental_path = "/objects/communications/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class EmailStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/email
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "emails"
    path = "/objects/emails"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = PropertiesList(
        Property("id", StringType),
        Property(
            "properties",
            ObjectType(
                Property("createdate", StringType),
                Property("hs_email_direction", StringType),
                Property("hs_email_sender_email", StringType),
                Property("hs_email_sender_firstname", StringType),
                Property("hs_email_sender_lastname", StringType),
                Property("hs_email_status", StringType),
                Property("hs_email_subject", StringType),
                Property("hs_email_text", StringType),
                Property("hs_email_to_email", StringType),
                Property("hs_email_to_firstname", StringType),
                Property("hs_email_to_lastname", StringType),
                Property("hs_lastmodifieddate", StringType),
                Property("hs_timestamp", StringType),
                Property("hubspot_owner_id", StringType),
            ),
        ),
        Property("createdAt", StringType),
        Property("updatedAt", StringType),
        Property("archived", BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class MeetingStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/meetings
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "meetings"
    path = "/objects/meetings"
    incremental_path = "/objects/meetings/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class NoteStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/notes
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "notes"
    path = "/objects/notes"
    incremental_path = "/objects/notes/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PostalMailStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/postal-mail
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "postal_mail"
    path = "/objects/postal_mail"
    incremental_path = "/objects/postal_mail/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class TaskStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/tasks
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "tasks"
    path = "/objects/tasks"
    incremental_path = "/objects/tasks/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

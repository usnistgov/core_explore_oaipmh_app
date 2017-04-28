"""OAI-PMH Query builder class
"""
from bson.objectid import ObjectId
from core_explore_common_app.utils.query.mongo.query_builder import QueryBuilder


class OaiPmhQueryBuilder(QueryBuilder):
    """Query builder class
    """

    def add_list_metadata_formats_criteria(self, list_metadata_format_ids):
        """Adds a criteria on OaiHarvesterMetadataFormat.

        Args:
            list_metadata_format_ids: List of OaiHarvesterMetadataFormat ids.

        Returns:

        """
        self.criteria.append({'harvester_metadata_format': {'$in': [ObjectId(metadata_format_id)
                                                                    for metadata_format_id in
                                                                    list_metadata_format_ids]}})

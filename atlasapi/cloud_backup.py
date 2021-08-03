# Copyright (c) 2021 Matthew G. Monteleone
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Cloud Backups Modile

Provides access to Cloud Backups and Cloudbackup restore endpoints
"""

from enum import Enum
from typing import List, NewType, Optional
from datetime import datetime
from atlasapi.lib import ProviderName, ClusterType
from dateutil.parser import parse
from pprint import pprint
import logging

logger = logging.getLogger(name='Atlas_cloud_backup')


def try_date(str_in: str) -> Optional[datetime]:
    try:
        datetime_out = parse(str_in)
    except (ValueError, TypeError, AttributeError):
        logger.debug(f'Could not parse a date from : {str_in}')
        datetime_out = None
    return datetime_out


class SnapshotType(Enum):
    ONDEMAND = "On Demand"
    SCHEDULED = "Scheduled"


class SnapshotStatus(Enum):
    QUEUED = "Queued"
    INPROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"


test_data = {
    "cloudProvider": "AWS",
    "createdAt": "2021-07-31T02:02:25Z",
    "expiresAt": "2021-08-28T02:03:22Z",
    "id": "6104a8c6c1b4ef7788b5d8f0",
    "links": [
        {
            "href": "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b1e92c13b34b93b0230e6e1/clusters/pyAtlasTestCluster/backup/snapshots/6104a8c6c1b4ef7788b5d8f0",
            "rel": "self"
        },
        {
            "href": "https://cloud.mongodb.com/api/atlas/v1.0/groups/5b1e92c13b34b93b0230e6e1/clusters/pyAtlasTestCluster",
            "rel": "http://cloud.mongodb.com/cluster"
        }
    ],
    "mongodVersion": "4.2.15",
    "replicaSetName": "pyAtlasTestCluster",
    "snapshotType": "scheduled",
    "status": "completed",
    "storageSizeBytes": 14380134400,
    "type": "replicaSet"
}


class CloudBackupSnapshot(object):
    def __init__(self, id: Optional[str] = None,
                 cloud_provider: Optional[ProviderName] = None,
                 created_at: Optional[datetime] = None,
                 description: Optional[str] = None,
                 expires_at: Optional[datetime] = None,
                 links: Optional[List] = None,
                 masterkey_uuid: Optional[str] = None,
                 members: Optional[list] = None,
                 mongod_version: Optional[str] = None,
                 replica_set_name: Optional[str] = None,
                 snapshot_ids: Optional[list] = None,
                 snapshot_type: Optional[SnapshotType] = None,
                 status: Optional[SnapshotStatus] = None,
                 storage_size_bytes: Optional[int] = None,
                 type: Optional[ClusterType] = None):
        """
        Details of a Cloud Provider Snapshot.

        Args:
            id: Unique identifier of the snapshot.
            cloud_provider: Cloud provider that stores this snapshot. Atlas returns this parameter when "type": "replicaSet".
            created_at:
            description: Description of the snapshot. Atlas returns this parameter when "status": "onDemand".
            expires_at:
            links: One or more links to sub-resources and/or related resources. The relations between URLs are
                   explained in the Web Linking Specification
            masterkey_uuid: Unique identifier of the AWS KMS Customer Master Key used to encrypt the snapshot.
                            Atlas returns this value for clusters using Encryption at Rest via Customer KMS.
            members: List of snapshots and the cloud provider where the snapshots are stored.
                     Atlas returns this parameter when "type": "shardedCluster".
            mongod_version:
            replica_set_name: Label given to the replica set from which Atlas took this snapshot.
                              Atlas returns this parameter when "type": "replicaSet".
                              snapshot_ids: Unique identifiers of the snapshots created for the shards and config server
                              for a sharded cluster. Atlas returns this parameter when "type": "shardedCluster".
                              These identifiers should match those given in the members[n].id parameters.
                              This allows you to map a snapshot to its shard or config server name.
            snapshot_type: Type of snapshot. Atlas can return onDemand or scheduled.
            status: Current status of the snapshot. Atlas can return one of the following values:
                    (queued, inProgress, completed, failed)
            storage_size_bytes:
            type: Type of cluster. Atlas can return replicaSet or shardedCluster.


        """
        self.type: Optional[ClusterType] = type
        self.storage_size_bytes: Optional[int] = storage_size_bytes
        self.status: Optional[SnapshotStatus] = status
        self.snapshot_type: Optional[SnapshotType] = snapshot_type
        self.snapshot_ids: Optional[list] = snapshot_ids
        self.replica_set_name: Optional[str] = replica_set_name
        self.mongod_version: Optional[str] = mongod_version
        self.members: Optional[list] = members
        self.masterkey_uuid: Optional[str] = masterkey_uuid
        self.links: Optional[list] = links
        self.expires_at: Optional[datetime] = expires_at
        self.description: Optional[str] = description
        self.created_at: Optional[datetime] = created_at
        self.cloud_provider: Optional[ProviderName] = cloud_provider
        self.id: Optional[str] = id

    @classmethod
    def from_dict(cls, data_dict: dict):
        id = data_dict.get('id', None)
        try:
            cloud_provider = ProviderName[data_dict.get('cloudProvider')]
        except KeyError:
            cloud_provider = ProviderName.TENANT
        created_at = try_date(data_dict.get('createdAt'))
        expires_at = try_date(data_dict.get('expiresAt'))
        description = data_dict.get('description')
        snapshot_type = SnapshotType[data_dict.get('snapshotType').upper()]
        cluster_type = ClusterType[data_dict.get('type').upper()]
        snapshot_status = SnapshotStatus[data_dict.get('status').upper()]
        storage_size_bytes = data_dict.get('storageSizeBytes')
        replica_set_name = data_dict.get('replicaSetName')
        links = data_dict.get('links')
        masterkey = data_dict.get('masterKeyUUID')
        members = data_dict.get('members')
        mongod_version = data_dict.get('mongodVersion')
        snapshot_ids = data_dict.get('snapshotIds')
        return cls(id=id,
                   cloud_provider=cloud_provider,
                   created_at=created_at,
                   expires_at=expires_at,
                   description=description,
                   snapshot_type=snapshot_type,
                   type=cluster_type,
                   status=snapshot_status,
                   storage_size_bytes=storage_size_bytes,
                   replica_set_name=replica_set_name,
                   links=links,
                   masterkey_uuid=masterkey,
                   members=members,
                   mongod_version=mongod_version,
                   snapshot_ids=snapshot_ids
                   )


test = CloudBackupSnapshot.from_dict(test_data)

pprint(test.__dict__)

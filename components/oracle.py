from components.providers import providers
import pulumi
from pulumi import ResourceOptions
from typing import Optional
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.core.v1 import (PersistentVolume, PersistentVolumeClaim, PersistentVolumeClaimSpecArgs, PersistentVolumeSpecArgs,
                                       LocalVolumeSourceArgs, ResourceRequirementsArgs, VolumeNodeAffinityArgs,
                                       NodeSelectorArgs, NodeSelectorTermArgs,NodeSelectorRequirementArgs,
                                       PodTemplateSpecArgs, PodSpecArgs, ContainerArgs, ContainerPortArgs,
                                       EnvVarArgs, LocalObjectReferenceArgs, VolumeArgs, HostPathVolumeSourceArgs,
                                       VolumeMountArgs, Service, ServiceSpecArgs, ServiceSpecType,
                                       ServicePortArgs, ProbeArgs, ExecActionArgs)
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs

class Oracle_k8s(pulumi.ComponentResource):
    def __init__(self, props: Optional["Inputs"] = None) -> None:
        super().__init__(t="Oracle_k8s", name="Oracle_k8s", props=props, opts=ResourceOptions(provider=providers.k8s_flink_local))

        child_opts = ResourceOptions(parent=self)

        self.oracle = Deployment(
            resource_name="oracle-resource",
            api_version="apps/v1",
            kind="Deployment",
            metadata=ObjectMetaArgs(
                name="oracle-db",
                labels={"app": "oracle-db"},
            ),
            spec=DeploymentSpecArgs(
                replicas=1,
                selector=LabelSelectorArgs(
                    match_labels={"app": "oracle-db"},
                ),
                template=PodTemplateSpecArgs(
                    metadata=ObjectMetaArgs(
                        labels={"app": "oracle-db"},
                    ),
                    spec=PodSpecArgs(
                        containers=[ContainerArgs(
                            name="oracle-db",
                            image="sgostiev/oracle:19.3.0-ee",
                            ports=[ContainerPortArgs(
                                container_port=1521,
                                host_port=1521,
                            ),],
                            volume_mounts=[
                                #  The data volume to use for the database.
                                VolumeMountArgs(mount_path="/opt/oracle/oradata", name="datamount"),
                            ],
                            image_pull_policy="IfNotPresent",
                            #resources=ResourceRequirementsArgs(
                            #    requests={"memory": "8Gi"},
                            #),
                            env=[EnvVarArgs(name="ORACLE_SID", value="ORCL"),
                                 EnvVarArgs(name="ORACLE_PDB", value="ORCLPDB1"),
                                 EnvVarArgs(name="ORACLE_PWD", value="MyPass123"),
                                 ],
                            readiness_probe=ProbeArgs(
                                initial_delay_seconds=3000,
                                timeout_seconds=6000,
                                failure_threshold=3,
                                success_threshold=1,
                                exec_=ExecActionArgs(
                                    command=[
                                        "bash",
                                        #"/opt/oracle/checkDBStatus.sh"
                                    ]
                                ),
                            ),
                        ),],
                        volumes=[VolumeArgs(name="datamount", 
                                            host_path=HostPathVolumeSourceArgs(
                                                path="/tdata/volumes",
                                                ),
                                            ),],
                    ),
                )
            ),
            opts=ResourceOptions(depends_on=[
                #flink_pvc
                ]).merge(child_opts),
        )

        self.oracle_service = Service(
            resource_name="oracle-service-resource",
            api_version="v1",
            metadata=ObjectMetaArgs(
                name="oracle-db",
            ),
            spec=ServiceSpecArgs(
                selector={"app": "oracle-db"},
                type=ServiceSpecType.NODE_PORT,
                ports=[
                    ServicePortArgs(name="listener",
                                    protocol="TCP",
                                    port=1521,
                                    target_port=1521),
                    ServicePortArgs(name="oemexpress",
                                    protocol="TCP",
                                    port=5500,
                                    target_port=5500),
                ],
            ),
            opts=ResourceOptions(depends_on=[
                self.oracle,
                ]).merge(child_opts),
        )

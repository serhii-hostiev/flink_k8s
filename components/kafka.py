from components.providers import providers
import pulumi
from pulumi import ResourceOptions
from typing import Optional
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.core.v1 import (PersistentVolume, PersistentVolumeClaim, PersistentVolumeClaimSpecArgs, PersistentVolumeSpecArgs,
                                       LocalVolumeSourceArgs, ResourceRequirementsArgs, VolumeNodeAffinityArgs,
                                       NodeSelectorArgs, NodeSelectorTermArgs,NodeSelectorRequirementArgs)
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs

class Kafka_k8s(pulumi.ComponentResource):
    def __init__(self, props: Optional["Inputs"] = None) -> None:
        super().__init__(t="Kafka_k8s", name="Kafka_k8s", props=props, opts=ResourceOptions(provider=providers.k8s_flink_local))

        child_opts = ResourceOptions(parent=self)

        self.kafka = Release(
            resource_name="kafka-resource",
            args=ReleaseArgs(
                chart="kafka",
                #version="19.13.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://charts.bitnami.com/bitnami",
                ),
                value_yaml_files=[pulumi.FileAsset("./components/helm_values/kafka_values.yml")],
            ),
            opts=ResourceOptions(depends_on=[
                #flink_pvc
                ]).merge(child_opts),
        )


        self.schema_registry = Release(
            resource_name="schema-registry-resource",
            args=ReleaseArgs(
                chart="schema-registry",
                #version="19.13.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://charts.bitnami.com/bitnami",
                ),
                value_yaml_files=[pulumi.FileAsset("./components/helm_values/schema_registry_values.yml")],
            ),
            opts=ResourceOptions(depends_on=[
                self.kafka,
                ]).merge(child_opts),
        )


        self.kafka_connect = Release(
            resource_name="kafka-connect-resource",
            args=ReleaseArgs(
                chart="kafka-connect",
                #version="19.13.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://licenseware.github.io/charts/",
                ),
                value_yaml_files=[pulumi.FileAsset("./components/helm_values/kafka_connect_values.yml")],
            ),
            opts=ResourceOptions(depends_on=[
                self.kafka,
                ]).merge(child_opts),
        )

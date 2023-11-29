from components.providers import providers
import pulumi
from pulumi import ResourceOptions
from typing import Optional
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.core.v1 import (PersistentVolume, PersistentVolumeClaim, PersistentVolumeClaimSpecArgs, PersistentVolumeSpecArgs,
                                       LocalVolumeSourceArgs, ResourceRequirementsArgs, VolumeNodeAffinityArgs,
                                       NodeSelectorArgs, NodeSelectorTermArgs,NodeSelectorRequirementArgs)
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs

class Kafka_ui_k8s(pulumi.ComponentResource):
    def __init__(self, props: Optional["Inputs"] = None) -> None:
        super().__init__(t="Kafka_ui_k8s", name="Kafka_ui_k8s", props=props, opts=ResourceOptions(provider=providers.k8s_flink_local))

        child_opts = ResourceOptions(parent=self)

        self.kafka_ui = Release(
            resource_name="kafka-ui-resource",
            args=ReleaseArgs(
                chart="kafka-ui",
                #version="19.13.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://provectus.github.io/kafka-ui-charts",
                ),
                value_yaml_files=[pulumi.FileAsset("./components/helm_values/kafka_ui_values.yml")],
            ),
            opts=ResourceOptions(depends_on=[
                #self.kafka,
                ]).merge(child_opts),
        )


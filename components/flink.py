from components.providers import providers
import pulumi
from pulumi import ResourceOptions
from typing import Optional
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.core.v1 import (PersistentVolume, PersistentVolumeClaim, PersistentVolumeClaimSpecArgs, PersistentVolumeSpecArgs,
                                       LocalVolumeSourceArgs, ResourceRequirementsArgs, VolumeNodeAffinityArgs,
                                       NodeSelectorArgs, NodeSelectorTermArgs,NodeSelectorRequirementArgs)
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs, LabelSelectorArgs

class Flink_k8s(pulumi.ComponentResource):
    def __init__(self, props: Optional["Inputs"] = None) -> None:
        super().__init__(t="Flink_k8s", name="Flink_k8s", props=props, opts=ResourceOptions(provider=providers.k8s_flink_local))

        child_opts = ResourceOptions(parent=self)

        self.elastic = Release(
            resource_name="flink-resource",
            args=ReleaseArgs(
                chart="flink",
                #version="19.13.0",
                repository_opts=RepositoryOptsArgs(
                    repo="https://charts.bitnami.com/bitnami",
                ),
                value_yaml_files=[pulumi.FileAsset("./components/helm_values/flink_values.yml")],
            ),
            opts=ResourceOptions(depends_on=[
                #flink_pvc
                ]).merge(child_opts),
        )


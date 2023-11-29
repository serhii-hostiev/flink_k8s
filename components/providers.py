from pulumi_kubernetes.provider import Provider


class Providers():
    def __init__(self) -> None:

        self.k8s_flink_local = Provider(
            resource_name="k8s_provider",
            kubeconfig="~/.kube/config",
            cluster="flink",
        )

providers = Providers()

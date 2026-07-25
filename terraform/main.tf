resource "kubernetes_namespace" "enterprise" {

  metadata {
    name = var.namespace
  }
}


resource "kubernetes_deployment" "app" {

  metadata {
    name = var.app_name
    namespace = var.namespace
  }

  spec {

    replicas = 2

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {

      metadata {
        labels = {
          app = var.app_name
        }
      }

      spec {

        container {

          name  = var.app_name
          image = "enterprise-devops-platform:latest"

          port {
            container_port = 5000
          }

        }
      }
    }
  }
}
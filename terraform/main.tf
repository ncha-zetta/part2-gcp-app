data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "${path.module}/function.zip"
}

resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = var.zip_file
  bucket       = var.app_bucket_name

  depends_on = [
    data.archive_file.source
  ]
}

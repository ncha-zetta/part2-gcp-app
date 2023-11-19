data "archive_file" "source" {
  type        = "zip"
  source_dir  = "../src"
  output_path = "${path.module}/function.zip"
}

resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"
  name         = "part2_cloud_function.zip"
  bucket       = google_storage_bucket.app_bucket.name

  depends_on = [
    google_storage_bucket.app_bucket,
    data.archive_file.source
  ]
}

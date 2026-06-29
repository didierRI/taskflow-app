import unittest

from api.project_metadata import archive_project_record, build_project_record


class ProjectMetadataTests(unittest.TestCase):
    def test_build_project_record_includes_workspace_and_timestamps(self):
        project = build_project_record(
            "proj_9",
            "Launch Plan",
            workspace_id="ws_2",
            timestamp="2026-06-29T18:30:00Z",
        )

        self.assertEqual(
            project,
            {
                "id": "proj_9",
                "name": "Launch Plan",
                "workspace_id": "ws_2",
                "archived": False,
                "created_at": "2026-06-29T18:30:00Z",
                "updated_at": "2026-06-29T18:30:00Z",
            },
        )

    def test_archive_project_record_marks_project_archived(self):
        project = build_project_record(
            "proj_9",
            "Launch Plan",
            workspace_id="ws_2",
            timestamp="2026-06-29T18:30:00Z",
        )

        archived = archive_project_record(project, timestamp="2026-06-29T19:00:00Z")

        self.assertTrue(archived["archived"])
        self.assertEqual(archived["archived_at"], "2026-06-29T19:00:00Z")
        self.assertEqual(archived["updated_at"], "2026-06-29T19:00:00Z")
        self.assertFalse(project["archived"])


if __name__ == "__main__":
    unittest.main()

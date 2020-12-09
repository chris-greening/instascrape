"""
Parse data related to comments, including comments in a thread
"""

import datetime


class Comment:
    """A single comment and its respective data"""

    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    def __init__(self, comment_dict: dict) -> None:
        self.comment_dict = comment_dict["node"]

        self._parse_data()

    def __repr__(self) -> str:
        return f"<Comment: {self.username}: {self.text}"

    def _parse_data(self) -> None:
        self.text = self.comment_dict["text"]
        self.created_at = datetime.datetime.fromtimestamp(self.comment_dict["created_at"])
        self.did_report_as_spam = self.comment_dict["did_report_as_spam"]
        self.is_verified = self.comment_dict["owner"]["is_verified"]
        self.profile_pic_url = self.comment_dict["owner"]["profile_pic_url"]
        self.username = self.comment_dict["owner"]["username"]
        self.viewer_has_liked = self.comment_dict["viewer_has_liked"]
        self.likes = self.comment_dict["edge_liked_by"]["count"]
        self.is_restricted_pending = self.comment_dict["is_restricted_pending"]

        try:
            comments = self.comment_dict["edge_threaded_comments"]["edges"]
            self.replies = [Comment(comment_dict) for comment_dict in comments]
        except KeyError:
            self.replies = []

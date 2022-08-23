from abc import ABC


class Database(ABC):
    
    def connect(self, *args, **kwargs):
        """Connection method for the database"""

    def create(self, *args, **kwargs):
        """Create a record/document in the table"""

    def get(self, *args, **kwargs):
        """Get a list of records that matches the criteria"""

    def retrieve(self, *args, **kwargs):
        """Retrieve a single record that matches the criteria"""

    def delete(self, *args, **kwargs):
        """Delete a record that matches the criteria"""

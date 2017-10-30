import config

class ModelSerializer(object):
    """
    Generic model serializer.
    """
    def __init__(self, model, fields=None):
        if fields is None:
            fields = []
        self.fields = fields
        self.model = model

    def build_response(self):
        """
        Method for building a complete response based on the JSON API spec:
        http://jsonapi.org/format/

        Returns:
            (dict)
        """
        return {
            "links": {
                "self": "http://example.com/{}/{}".format(
                    self.get_type_name(self.model),
                    self.model.id
                ),
            },
            "data": self.serialize_model_object(),
            "relationships": self.get_relationships()
        }

    def serialize_model_object(self):
        """
        Serializes a single model object.
        Returns:
            (dict)
        """
        return {
            'type': self.get_type_name(self.model),
            'id': self.model.id,
            'attributes': self.get_attributes()
        }

    @staticmethod
    def get_type_name(model_obj):
        """
        Gets the class name of an object and return the JSON API spec compliant type name.

        Args:
            model_obj: A model object

        Returns:
            (str)
        """
        return model_obj.__class__.__name__.lower() + 's'

    def get_attributes(self):
        """
        Get the serialized attributes from a model. Attributes to be serialized are defined in
        ``self.fields``.

        Returns:
            (dict)
        """
        return {
            attr: getattr(self.model, attr) for attr in dir(self.model) if attr in self.fields
        }

    def build_links(self):
        return config.DOMAIN + '/{}/{}'.format(
            self.get_type_name(self.model),
            self.model.id
        )

    def get_relationships(self):
        return {
            "messages": {
                "links": {
                    "self": "self"
                },
                "data": [
                    {"type": "users", "id": 1},
                    {"type": "users", "id": 1}
                ]
            }
        }

    def get_included(self):
        raise NotImplemented()

    def update_model(self, data):
        for key, val in data.items():
            if key in self.fields:
                setattr(self.model, key, val)


s = {
  "links": {
    "self": "http://example.com/articles",
    "next": "http://example.com/articles?page[offset]=2",
    "last": "http://example.com/articles?page[offset]=10"
  },
  "data": [
      {
        "type": "articles",
        "id": "1",
        "attributes": {
          "title": "JSON API paints my bikeshed!"
        },
        "relationships": {
          "author": {
            "links": {
              "self": "http://example.com/articles/1/relationships/author",
              "related": "http://example.com/articles/1/author"
            },
            "data": { "type": "people", "id": "9" }
          },
          "comments": {
            "links": {
              "self": "http://example.com/articles/1/relationships/comments",
              "related": "http://example.com/articles/1/comments"
            },
            "data": [
              { "type": "comments", "id": "5" },
              { "type": "comments", "id": "12" }
            ]
          }
        },
        "links": {
          "self": "http://example.com/articles/1"
        }
  }
  ],
  "included": [
    {
    "type": "people",
    "id": "9",
    "attributes": {
      "first-name": "Dan",
      "last-name": "Gebhardt",
      "twitter": "dgeb"
    },
    "links": {
      "self": "http://example.com/people/9"
    }
  }, {
    "type": "comments",
    "id": "5",
    "attributes": {
      "body": "First!"
    },
    "relationships": {
      "author": {
        "data": { "type": "people", "id": "2" }
      }
    },
    "links": {
      "self": "http://example.com/comments/5"
    }
  }, {
    "type": "comments",
    "id": "12",
    "attributes": {
      "body": "I like XML better"
    },
    "relationships": {
      "author": {
        "data": { "type": "people", "id": "9" }
      }
    },
    "links": {
      "self": "http://example.com/comments/12"
    }
  }]
}


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
                "self": "/{}/{}".format(
                    self.get_type_name(self.model, plural=True),
                    self.model.pk
                ),
            },
            "data": self.serialize_model_object(),
        }

    def serialize_model_object(self):
        """
        Serializes a single model object.
        Returns:
            (dict)
        """
        return {
            'type': self.get_type_name(self.model),
            'id': self.model.pk,
            'attributes': self.get_attributes()
        }

    @staticmethod
    def get_type_name(model_obj, plural=False):
        """
        Gets the class name of an object and return the JSON API spec compliant type name.

        Args:
            model_obj: A model object

        Returns:
            (str)
        """
        type_name = model_obj.__class__.__name__.lower()
        if plural:
            type_name += "s"
        return type_name

    def get_attributes(self):
        """
        Get the serialized attributes from a model. Attributes to be serialized are defined in
        ``self.fields``.

        Returns:
            (dict)
        """
        return {
            attr: getattr(self.model, attr, None) for attr in dir(self.model) if attr in self.fields
        }

    def build_links(self):
        return config.DOMAIN + '/{}/{}'.format(
            self.get_type_name(self.model, plural=True),
            self.model.pk
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

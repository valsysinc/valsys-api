from http import HTTPStatus


class ModelingServiceClientException(Exception):
    def __init__(self, data: str, status_code: HTTPStatus, url: str) -> None:
        self.url = url
        self.status_code = status_code
        self.data = data
        super().__init__(f"{self.url} {self.data} {self.status_code}")

    def jsonify(self):
        return {
            "url": self.url,
            "status_code": self.status_code,
            "data": str(self.data),
        }

    def __repr__(self):
        return str(self.jsonify())


class ModelingServiceGetException(ModelingServiceClientException):
    pass


class ModelingServicePostException(ModelingServiceClientException):
    pass

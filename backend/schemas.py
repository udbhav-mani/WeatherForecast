from marshmallow import Schema, fields


class LocationSchema(Schema):
    cityname = fields.Str()
    country = fields.Str()
    lat = fields.Float()
    lon = fields.Float()
    localtime = fields.Time()


class AstroSchema(Schema):
    sunrise = fields.Time(required=True)
    sunset = fields.Time(required=True)


class WeatherSchema(Schema):
    temp = fields.Float(required=True)
    max_temp = fields.Float(required=True)
    min_temp = fields.Float(required=True)
    feels_like = fields.Float(required=True)
    pressure = fields.Float(required=True)
    humidity = fields.Float(required=True)
    astro = fields.Nested(AstroSchema, dump_only=True)
    location = fields.Nested(LocationSchema, dump_only=True)


class PollutionSchema(Schema):
    location = fields.Nested(LocationSchema, dump_only=True)
    aqi = fields.Float(required=True)
    pm25 = fields.Float(required=True)
    pm10 = fields.Float(required=True)
    so2 = fields.Float(required=True)
    no2 = fields.Float(required=True)
    co = fields.Float(required=True)

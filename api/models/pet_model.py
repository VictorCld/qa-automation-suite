class PetSchema:
    REQUIRED_FIELDS = {"id", "name", "status", "photoUrls"}
    VALID_STATUSES = {"available", "pending", "sold"}

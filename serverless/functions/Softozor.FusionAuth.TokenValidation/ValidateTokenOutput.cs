namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record ValidateTokenOutput([property: JsonPropertyName("user_id")] Guid UserId);
namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record ValidateTokenOutput([property: JsonPropertyName("userId")] Guid UserId);
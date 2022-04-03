namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record SetPasswordOutput([property: JsonPropertyName("userId")] Guid UserId);
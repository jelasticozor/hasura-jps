namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record ValidateTokenOutput([property: JsonProperty("user_id")] Guid UserId);
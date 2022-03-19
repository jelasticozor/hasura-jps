namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record ValidateTokenOutput([property: JsonProperty("userId")] Guid UserId);

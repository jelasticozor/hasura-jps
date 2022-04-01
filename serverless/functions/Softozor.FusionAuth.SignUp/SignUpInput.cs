namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record SignUpInput(
    [property: JsonProperty("email")] string Email,
    [property: JsonProperty("role")] string Role,
    [property: JsonProperty("appId")] Guid AppId);
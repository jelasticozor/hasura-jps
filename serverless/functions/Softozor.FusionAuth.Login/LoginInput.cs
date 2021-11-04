namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record LoginInput(
    [property: JsonProperty("username")] string Username,
    [property: JsonProperty("password")] string Password,
    [property: JsonProperty("appId")] Guid AppId);
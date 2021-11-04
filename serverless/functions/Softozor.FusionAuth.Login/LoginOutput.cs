namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record LoginOutput(
    [property: JsonProperty("token")] string Token,
    [property: JsonProperty("userId")] Guid UserId);
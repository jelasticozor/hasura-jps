namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record SetPasswordOutput(
    [property: JsonProperty("userId")] Guid UserId);

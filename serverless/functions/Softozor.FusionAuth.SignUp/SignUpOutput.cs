namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record SignUpOutput(
    [property: JsonProperty("userId")] Guid UserId);

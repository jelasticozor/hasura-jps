namespace HasuraFunction;

using System;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public static class AppSetup
{
    private const string DefaultAccessTokenAuthHeaderPrefix = "Bearer";

    [SuppressMessage(
        "Design",
        "CA1031: Do not catch general exception types",
        Justification =
            "That's the last step before outputting to the user, therefore we need to catch everything and return a useful error message")]
    public static void Configure(WebApplication app)
    {
        app.MapPost(
            "/",
            async (HttpContext http, IActionHandler<BearerTokenAuthorizationHeader, ValidateTokenOutput> handler) =>
            {
                var input = ExtractInput(http);

                try
                {
                    var output = await handler.Handle(input);
                    await http.Response.WriteAsJsonAsync(output);
                }
                catch (HasuraFunctionException ex)
                {
                    await ActionHandlerWrapper.IssueError(http, ex);
                }
                catch (Exception ex)
                {
                    await ActionHandlerWrapper.IssueInternalServerError(http, ex);
                }
            });
    }

    private static BearerTokenAuthorizationHeader ExtractInput(HttpContext http)
    {
        var authorization = http.Request.Headers["Authorization"].FirstOrDefault();

        if (string.IsNullOrWhiteSpace(authorization))
        {
            throw new HasuraFunctionException(
                "The request contains no authorization header",
                StatusCodes.Status400BadRequest);
        }

        if (!authorization.StartsWith(DefaultAccessTokenAuthHeaderPrefix, StringComparison.OrdinalIgnoreCase))
        {
            throw new HasuraFunctionException(
                "The authorization header does not contain a Bearer token",
                StatusCodes.Status400BadRequest);
        }

        var token = authorization.Substring(DefaultAccessTokenAuthHeaderPrefix.Length).Trim();

        return new BearerTokenAuthorizationHeader(token);
    }
}
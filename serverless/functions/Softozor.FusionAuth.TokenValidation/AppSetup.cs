namespace HasuraFunction;

using System;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Serilog;
using Softozor.HasuraHandling;

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
        app.UseSerilogRequestLogging();

        app.MapPost(
            "/",
            async (HttpContext http, ILoggerFactory loggerFactory, ValidateTokenHandler handler) =>
            {
                var logger = loggerFactory.CreateLogger("root");

                try
                {
                    var input = ExtractInput(http);
                    await handler.Handle(input);
                    await http.Response.WriteAsJsonAsync(new ValidateTokenOutput(true));
                }
                catch (HasuraFunctionException ex)
                {
                    logger.LogError(ex, "an error occurred");
                    await ErrorReporter.ReportError(http, ex);
                }
                catch (Exception ex)
                {
                    logger.LogError(ex, "an unexpected error occurred");
                    await ErrorReporter.ReportUnexpectedError(http, ex);
                }
                finally
                {
                    Log.CloseAndFlush();
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
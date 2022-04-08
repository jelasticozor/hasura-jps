namespace HasuraFunction;

using System;
using System.Diagnostics.CodeAnalysis;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Serilog;
using Softozor.HasuraHandling;

public static class AppSetup
{
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
            async (HttpContext http, ILoggerFactory loggerFactory, SignInHandler handler) =>
            {
                var logger = loggerFactory.CreateLogger("root");

                try
                {
                    var input = await InputHandling.ExtractActionRequestPayloadFrom<SignInInput>(http);
                    var (signInOutput, refreshToken) = await handler.Handle(input);
                    await http.Response.WriteAsJsonAsync(signInOutput);
                    http.Response.Cookies.Append(
                        "refresh-token",
                        refreshToken,
                        new CookieOptions { Expires = DateTimeOffset.Now.AddDays(1), MaxAge = TimeSpan.FromDays(1) });
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
}
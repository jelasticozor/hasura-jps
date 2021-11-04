namespace HasuraFunction;

using System;
using System.Diagnostics.CodeAnalysis;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Softozor.HasuraHandling;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public static class AppSetup
{
    [SuppressMessage(
        "Design",
        "CA1031: Do not catch general exception types",
        Justification =
            "That's the last step before outputting to the user, therefore we need to catch everything and return a useful error message")]
    public static void Configure(WebApplication app)
    {
        app.MapPost(
            "/",
            async (HttpContext http, IActionHandler<LoginInput, (LoginOutput, string)> handler) =>
            {
                var input = await ActionHandlerWrapper.ExtractInput<LoginInput>(http);

                try
                {
                    var (loginOutput, refreshToken) = await handler.Handle(input);
                    await http.Response.WriteAsJsonAsync(loginOutput);
                    http.Response.Cookies.Append(
                        "refresh-token",
                        refreshToken,
                        new CookieOptions { Expires = DateTimeOffset.Now.AddDays(1), MaxAge = TimeSpan.FromDays(1) });
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
}
namespace HasuraFunction;

using System;
using System.Diagnostics.CodeAnalysis;
using System.Threading.Tasks;
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
            async (HttpContext http, IActionHandler<SetPasswordInput, SetPasswordOutput> handler) =>
            {
                Func<SetPasswordInput, Task<SetPasswordOutput>> handleFn = handler.Handle;
                await ActionHandlerWrapper.HandleAsync(http, handleFn);
            });
    }
}
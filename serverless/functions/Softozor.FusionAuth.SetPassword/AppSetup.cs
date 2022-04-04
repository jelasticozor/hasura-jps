namespace HasuraFunction;

using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Softozor.HasuraHandling;
using Softozor.HasuraHandling.Interfaces;

public static class AppSetup
{
    public static void Configure(WebApplication app)
    {
        app.MapPost(
            "/",
            async (HttpContext http, SetPasswordHandler handler) =>
            {
                var handleFn = handler.Handle;
                await ActionHandlerWrapper.HandleAsync(http, handleFn);
            });
    }
}
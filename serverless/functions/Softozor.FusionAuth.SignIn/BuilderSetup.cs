namespace HasuraFunction;

using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;
using Softozor.FusionAuth;
using Softozor.HasuraHandling.Interfaces;

public static class BuilderSetup
{
    public static void Configure(WebApplicationBuilder builder)
    {
        builder.Services.AddDataProtection();

        builder.Services.AddAutoMapper(typeof(BuilderSetup));

        builder.Services.AddFusionAuthClient();

        builder.Services.AddTransient(
                srvProvider =>
                {
                    var secretReader = srvProvider.GetService<ISecretReader>();
                    var provider = srvProvider.GetService<IDataProtectionProvider>();
                    var dataProtectionSecret = secretReader!.GetSecret(FaasKeys.DataProtectionSecret);
                    return provider!.CreateProtector(dataProtectionSecret);
                })
            .AddTransient<IActionHandler<SignInInput, (SignInOutput, string)>, SignInHandler>();
    }
}
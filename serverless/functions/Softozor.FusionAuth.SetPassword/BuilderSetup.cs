namespace HasuraFunction;

using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using Serilog.Exceptions;
using Serilog.Sinks.Graylog;
using Softozor.FusionAuth;
using Softozor.HasuraHandling.ConfigurationManagement;

public static class BuilderSetup
{
    public static void Configure(WebApplicationBuilder builder)
    {
        ConfigureLogger(builder);

        builder.Services.AddConfigurationManagement().AddAutoMapper(typeof(BuilderSetup)).AddFusionAuthClient();

        builder.Services.AddTransient<SetPasswordHandler, SetPasswordHandler>();
    }

    private static void ConfigureLogger(WebApplicationBuilder builder)
    {
        var configuration = new LoggerConfiguration().Enrich.WithExceptionDetails().WriteTo.Console();

        var logsAggregatorHost = Environment.GetEnvironmentVariable("LOGS_AGGREGATOR_HOST");

        if (!string.IsNullOrWhiteSpace(logsAggregatorHost) && int.TryParse(
                Environment.GetEnvironmentVariable("LOGS_AGGREGATOR_PORT"),
                out var logsAggregatorPort))
        {
            configuration.WriteTo.Graylog(
                new GraylogSinkOptions { HostnameOrAddress = logsAggregatorHost, Port = logsAggregatorPort });
        }

        var logger = configuration.CreateLogger();
        builder.Host.UseSerilog(logger);
    }
}
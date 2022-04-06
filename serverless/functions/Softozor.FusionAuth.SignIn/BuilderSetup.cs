﻿namespace HasuraFunction;

using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using Serilog.Exceptions;
using Serilog.Sinks.Graylog;
using Serilog.Sinks.Graylog.Core.Transport;
using Softozor.FusionAuth;
using Softozor.HasuraHandling;
using Softozor.HasuraHandling.ConfigurationManagement;

public static class BuilderSetup
{
    public static void Configure(WebApplicationBuilder builder)
    {
        ConfigureLogger(builder);

        builder.Services.AddConfigurationManagement()
            .AddAutoMapper(typeof(BuilderSetup))
            .AddFusionAuthClient()
            .AddDataProtection();

        builder.Services.AddTransient(
                srvProvider =>
                {
                    var secretReader = srvProvider.GetService<ISecretReader>();
                    var provider = srvProvider.GetService<IDataProtectionProvider>();
                    var dataProtectionSecret = secretReader!.GetSecret(FaasKeys.DataProtectionSecret);
                    return provider!.CreateProtector(dataProtectionSecret);
                })
            .AddTransient<SignInHandler, SignInHandler>();
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
                new GraylogSinkOptions { HostnameOrAddress = logsAggregatorHost, Port = logsAggregatorPort, TransportType = TransportType.Udp });
        }

        var logger = configuration.CreateLogger();
        builder.Host.UseSerilog(logger);
    }
}
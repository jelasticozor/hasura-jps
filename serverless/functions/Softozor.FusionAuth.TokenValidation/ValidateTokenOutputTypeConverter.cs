namespace HasuraFunction;

using System;
using AutoMapper;
using io.fusionauth.domain.api.jwt;
using Newtonsoft.Json;
using Softozor.HasuraHandling.Data;

public class ValidateTokenOutputTypeConverter : ITypeConverter<ValidateResponse, ValidateTokenOutput>
{
    public ValidateTokenOutput Convert(
        ValidateResponse source,
        ValidateTokenOutput? destination,
        ResolutionContext context)
    {
        var hasuraClaimsNamespace = Environment.GetEnvironmentVariable("HASURA_CLAIMS_NAMESPACE");
        var serializedClaims = source.jwt[hasuraClaimsNamespace].ToString().Replace("\n", " ");
        ;
        var claims = JsonConvert.DeserializeObject<HasuraClaims>(serializedClaims);

        return new ValidateTokenOutput(claims.UserId);
    }
}
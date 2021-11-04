namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api.jwt;

public class TokenValidationProfile : Profile
{
    public TokenValidationProfile()
    {
        this.CreateMap<ValidateResponse, ValidateTokenOutput>().ConvertUsing<ValidateTokenOutputTypeConverter>();
    }
}
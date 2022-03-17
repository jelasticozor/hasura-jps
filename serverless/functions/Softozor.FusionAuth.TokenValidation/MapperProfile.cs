namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api.jwt;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<ValidateResponse, ValidateTokenOutput>().ConvertUsing<ValidateTokenOutputTypeConverter>();
    }
}
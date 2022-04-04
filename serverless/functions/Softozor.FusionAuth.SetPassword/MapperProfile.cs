namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api.user;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<SetPasswordInput, ChangePasswordRequest>()
            .ForMember(dest => dest.password, opt => opt.MapFrom(src => src.Password));
    }
}
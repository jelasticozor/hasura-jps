namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api.user;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<SetPasswordInput, ChangePasswordRequest>()
            .ForMember(dest => dest.applicationId, opt => opt.Ignore())
            .ForMember(dest => dest.currentPassword, opt => opt.Ignore())
            .ForMember(dest => dest.loginId, opt => opt.Ignore())
            .ForMember(dest => dest.refreshToken, opt => opt.Ignore())
            .ForMember(dest => dest.eventInfo, opt => opt.Ignore());
    }
}
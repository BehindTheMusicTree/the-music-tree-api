#!/usr/bin/env python


from django.contrib.auth.models import User

from bodzify_api.service.Service import Service


class TrackService(Service):

    # def _get_put_schema_serializer(self, old_instance, put_schema_data: QueryDict) -> Serializer:
    #     return TrackPutSchemaSerializer(instance=old_instance, data=put_schema_data) # type: ignore

    # def _get_save_model_serializer(self, old_instance, save_model_data: QueryDict, partial: bool) -> Serializer:
    #     return TrackSaveModelSerializer(instance=old_instance, data=save_model_data, partial=True) # type: ignore

    # def _get_save_schema_data_from_post_schema_data(self, post_schema_data: QueryDict) -> QueryDict:
    #     file = post_schema_data[TRACK_ATTRIBUTES_LABEL.FILE]
    #     save_schema_data_from_file = self._get_save_schema_data_from_file(file=file)
    #     save_schema_data = self._get_dict1_overriden_with_dict2_when_key_is_provided(
    #         dict1=save_schema_data_from_file, dict2=post_schema_data)

    #     if TRACK_ATTRIBUTES_LABEL.TITLE not in save_schema_data:
    #         filename = os.path.basename(file.name).split('.')[0]
    #         if TRACK_SCHEMA_ATTRIBUTES_LABEL.FORCE_TITLE_GENERATION in post_schema_data:
    #             force_title_generation = post_schema_data[TRACK_SAVE_SCHEMA_ATTRIBUTES_LABEL.FORCE_TITLE_GENERATION]
    #         else:
    #             force_title_generation = False

    #         if len(filename) > settings.TRACK_FILENAME_LENGTH_MAX or force_title_generation:
    #             title = settings.TRACK_GENERATED_TITLE_PREFIXE + \
    #                 self.generate_short_uu(settings.TRACK_GENERATED_TITLE_LEN -
    #                                 len(settings.TRACK_GENERATED_TITLE_PREFIXE))
    #         else:
    #             title = filename
    #         save_schema_data[TRACK_ATTRIBUTES_LABEL.TITLE] = title

    #     return save_schema_data

    # def _get_save_model_data_from_save_schema_data(self, user: User, save_schema_data: QueryDict) -> QueryDict:
    #     save_model_data = QueryDict(mutable=True)
    #     save_model_data[TRACK_ATTRIBUTES_LABEL.USER] = user.id

    #     save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
    #         key=TRACK_ATTRIBUTES_LABEL.FILE,
    #         querydict1=save_model_data,
    #         querydict2=save_schema_data)

    #     save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
    #         key=TRACK_ATTRIBUTES_LABEL.TITLE,
    #         querydict1=save_model_data,
    #         querydict2=save_schema_data)

    #     save_model_data = self._get_dict1_updated_with_artist_uuid_if_artist_name_in_dict2(
    #         user=user, dict1=save_model_data, dict2=save_schema_data)

    #     save_model_data = self._get_dict1_updated_with_album_uuid_if_album_name_in_dict2(
    #         user=user, dict1=save_model_data, dict2=save_schema_data)

    #     save_model_data = self._get_dict1_updated_with_genre_uuid_if_genre_name_in_dict2(
    #         user=user, dict1=save_model_data, dict2=save_schema_data)

    #     save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
    #         key=TRACK_ATTRIBUTES_LABEL.DURATION,
    #         querydict1=save_model_data,
    #         querydict2=save_schema_data)

    #     save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
    #         key=TRACK_ATTRIBUTES_LABEL.RATING,
    #         querydict1=save_model_data,
    #         querydict2=save_schema_data)

    #     save_model_data = self.get_querydict1_updated_with_querydict2_key_if_set(
    #         key=TRACK_ATTRIBUTES_LABEL.LANGUAGE,
    #         querydict1=save_model_data,
    #         querydict2=save_schema_data)

    #     return save_model_data

    def delete(self, user: User, instance):
        instance.delete_with_albums_and_tracks()

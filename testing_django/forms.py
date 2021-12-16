from django import forms


class PickTimesForm(forms.Form):
    start_date = forms.CharField()
    end_date = forms.CharField()


class PickTrackForm(forms.Form):
    track_number = forms.CharField()

    # def return_track_number(self):
    #     data = self.cleaned_data[your_track]
    #     # Remember to always return the cleaned data.
    #     return data




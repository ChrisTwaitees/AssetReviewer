from django import forms


# Search Form
class AssetViewerSettingsForm(forms.Form):
    attrs = {

    }


    #directories_dropdown = forms.ComboField()

    search_text = forms.CharField(label="Search",
                                  required=False,
                                  max_length=100,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'Search...',
                                      'style': 'width: 300px;'}))



Template.detail.helpers({
    getSuggestedApp: function(appId) {
        Meteor.subscribe('singleAppByAppId', appId);
        return Apps.findOne({app_id: appId});
    }
});

Template.detail.events({
    "click #backLink" : function(evt) {
        history.back();
    }
});
if(Apps.find({}).count() < 1){
    var fs = Npm.require('fs');
    fs.readFile('../../../../../testdata.json',
         'utf8', Meteor.bindEnvironment(function(error, data) {
        if (error) throw error;
        var appData = data.split("\n");
        for (var i = 0; i < appData.length - 1; i++) {
            var app = JSON.parse(appData[i]);
            app.iconUrl = app.thumbnail_url;
            app.avgRating = parseInt(app.score) / 2;
            app.recommendation = app.top_5_app;
            app.numberOfRecommendations = 0;
            Apps.insert(app);
        }
        var list = Apps.find({}, {fields: {top_5_app: 1}}).fetch();
        for (var i = 0; i < list.length; i++) {
            var top5 = list[i].top_5_app;
            if (top5) {
                for (var j = 0; j < top5.length; j++) {
                    Apps.update({app_id: top5[j]}, {$inc: {numberOfRecommendations: 1}});
                }
            }
        }
    }, function(error){
        throw error;
    }));
}

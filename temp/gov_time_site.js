// ONLOAD OPERATIONS FOR THE SITE
window.onload = function () {
  /* PARSE THE URL FOR 12/24 VARIABLE*/
  var getT = location.search;
  var tArr = getT.split("=");
  var t = tArr[1];

  // CREATE A VAR FOR THE CHECKBOX
  var twentyFour = document.getElementById("twenty-four");

  // CHECK VALUE OF 12/24 URL VAR "t" AND SET CHECKBOX ACCORDINGLY
  if (t === "24") {
    twentyFour.checked = true;
  } else {
    // DEFAULT TO 12HR DISPLAY
    twentyFour.checked = false;
  }

  var noMoreAlerts = false;
  // NOTIFICATION BOX FOR BOOKMARKING 24-HOUR SETTINGS PAGE
  var twentyFour = document.getElementById("twenty-four");
  twentyFour.addEventListener("click", function (event) {
    var hourLabelDiv = document.getElementsByClassName("am-pm")[0];
    var url = window.location.toString();
    if (timeDotGov.data.twentyFour()) {
      window.history.replaceState(url, "", "/?t=24");
      if (!noMoreAlerts) {
        alert(
          "Bookmarking this page will save your preference for 24-hour time display."
        );
      }
      noMoreAlerts = true;
    } else {
      window.history.replaceState(url, "", "/");
    }
    timeDotGov.clockController.handleonrefresh(new Date());
  });

  //?   timeZoneChange = function(event) {
  //?     timeDotGov.clockController.getnewOffset(event.target.value);
  //?   }

  // LOAD DST DATES AND LEAP DATE
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", "auxdata.xml", false); // false for synchronous request
  xmlHttp.send(null);
  timeDotGov.auxdata = xmlHttp.responseText;

  timeDotGov.clockController.auxdata();

  timeDotGov.clockController.checkservertime();
  document.getElementById("responseTime").innerHTML =
    timeDotGov.data.zoneOffset;

  // SET REFRESH RATE TO CHECK FOR TOP OF NEW SECOND, SO THE DISPLAY DOES NOT HAVE TO BE REFRESHED MORE THAN NECESSARY
  setInterval(function () {
    if (timeDotGov.data.currentTime) {
      timeDotGov.clockController.runningclocks();
    }
  }, 20); // 20 milliseconds

  // FUNCTION REFRESHES PAGE EVERY 10 MIN
  setInterval(function () {
    location.reload();
  }, 600000);
};

function lol()
{
  $( ".sidebarlink" ).click({param1: this}, blikejVoe);
  $( "#resetcookieslink" ).click({param1: this}, resetCookies);
  $('.cbox').each(function(index)
  {
    var cookie = Cookies.get(this.id);
    var cislo = this.id.split("_")[1];
    console.log(this.id + "; value = " + cookie);
    if(cookie === undefined) {
      if ( cislo === "holesovice" ) {
        cookie = 0
      }
      else {
        cookie = 1
      }
    }
    if(cookie == 0) {
      $("#" + this.id).prop("checked", false);
      $("." + cislo).hide(); // proč máš pro checkboxy idčka a pro listky classu lol
      if ( cislo === "holesovice" || cislo === "brumlovka" ) {
        $(".div_loc_" + cislo).hide();
      }
    }
    else {
      $("#" + this.id).prop("checked", true);
    }
  });

  $('.cbox').change(function(event) {
    var cislo = this.id.split("_")[1];
    if (this.checked) {
      Cookies.set(this.id, 1);
      $("." + cislo).fadeIn();
      if ( cislo === "holesovice" || cislo === "brumlovka" ) {
        $(".div_loc_" + cislo).fadeIn();
        $(".cbox_loc_" + cislo).prop("checked", true);
      }
    }
    else {
      Cookies.set(this.id, 0);
      $("." + cislo).fadeOut();
      if ( cislo === "holesovice" || cislo === "brumlovka" ) {
        $(".div_loc_" + cislo).fadeOut();
        $(".cbox_loc_" + cislo).prop("checked", false);
      }
    }
  });

  function blikejVoe(event) {
    var cislo = event.target.id.split("_")[1];
    $("." + cislo).effect("highlight", {color: "#4E88FF"}, 1500);
    Cookies.set("cbox_" + cislo, 1);
    $("#cbox_" + cislo).prop("checked", true);
  }

  function resetCookies() {
    $('.cbox').each(function() {
      Cookies.remove(this.id);
    });
    location.reload();
  }

  $(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
      $(this).toggleClass('active');
    });
  });
}

def header():
    header = '''Content-type:text/html; charset=utf-8\r\n\r\n
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="sv-SE">

<head profile="http://gmpg.org/xfn/11">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width" />

<title>Sök i statens offentliga utredningar</title>

<link rel="stylesheet" href="./style.css" type="text/css" media="screen" />

<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico">

<link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet">

<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>



<!-- Radio buttons by: http://cssdeck.com/user/ftntravis -->
	
<script type="text/javascript">
$(document).ready(function(){
    $('input[type="radio"]').click(function(){
        if($(this).attr("value")=="simple"){
            $(".box").not(".simple").hide();
            $(".simple").show();
        }
        if($(this).attr("value")=="advanced"){
            $(".box").not(".advanced").hide();
            $(".advanced").show();
        }
    });
});
</script>


</head>

<body>
	

	
	
<div id="sidebar">

<a href="/"><div id="top">
	
	<div class="toppadding">
	<span class="icon">&#9737;</span> <h1>Offentliga utredningar</h1>
	</div>
	
</div> <!-- / top --></a>


<div class="sidebarinside">


<div id="searchbar">	
	
<div id="searchfield">

<form action="search" method="get">
            <input type="text" name="q" value="'''
    return(header)

def header2():
    header2 = '''">


</div> <!-- / searchfield -->


<div id="searchoptions">

<div class="searchtype">
<input type="radio" name="method" id="radio1" class="radio" value="simple" checked/>
<label for="radio1">Enkel</label>
</div>

<div class="searchtype">
<input type="radio" name="method" id="radio2" class="radio" value="advanced" />
<label for="radio2">Avancerad</label>
</div>

</div> <!-- / searchoptions -->


<div id="utokadsokning">

    <div class="simple box"><!--Placeholder for 'enkel'--></div>
    <div class="advanced box">

    
    <h5>Datumordning, årtal</h5>
    <p><input type="radio" name="order" value="year asc" checked /> Stigande
    <input type="radio" name="order" value="year desc" /> Fallande</p>
	
    </div> <!-- / green box -->
    
</div> <!-- / utokadsokning -->    
    
    
    

<div id="searchbutton">	
<input type="submit" value="Utför sökning" class="sun-flower-button">
</div> <!-- / searchbutton -->
    
    
</div> <!-- / searchbar -->


</div> <!-- / sidebarinside -->
</div> <!-- / sidebar -->





<div id="topmaindiv">
<div class="topmaindivpadding">Ett gratis verktyg för att söka i statens offentliga utredningar. <a href="./om.html">Läs mer.</a></div>
</div>


	
<div id="maindiv">

    <div id="maindivcontent">
'''
    return(header2)



def insearchheader():
    insearchheader = '''<div id="resulttable"><div class="resultinfo">
	<div class="result1">
		<h3>Namn</h3>
	</div> <!-- / result1 -->

                <div class="result3">
                        <h3>PDF</h3>
                </div> <!-- / result3 -->

                <div class="result2">
                        <h3>Publicerad</h3>
                </div> <!-- / result2 -->
        </div> <!-- / result -->'''
    return(insearchheader)


def footer():
    footer = '''
    </div> <!-- / resulttable -->	
    </div> <!-- / maindivcontent -->
    </div> <!-- / maindiv -->
    </body>
    </html>
    '''
    return(footer)

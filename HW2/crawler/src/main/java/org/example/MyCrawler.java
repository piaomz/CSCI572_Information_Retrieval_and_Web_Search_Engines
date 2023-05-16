package org.example;


import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;


import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

import com.opencsv.CSVWriter;
public class MyCrawler extends WebCrawler {
    private HashSet<String> visitedURLs = new HashSet<>();
    private final static Pattern FILTERS = Pattern.compile(
            ".*(\\.(" + "css|js|json|webmanifest|ttf|svg|wav|avi|mov|mpeg|mpg|ram|m4v|wma|wmv|mid|txt|mp2|mp3|mp4|zip|rar|gz|exe|ico))$");
    private static CSVWriter fetchFile;
    private static CSVWriter visitFile;
    private static CSVWriter urlsFile;
    private static int fetchCount;

    /**
     * This method receives two parameters. The first parameter is the page
     * in which we have discovered this new url and the second parameter is
     * the new url. You should implement this function to specify whether
     * the given url should be crawled or not (based on your crawling logic).
     * In this example, we are instructing the crawler to ignore urls that
     * have css, js, git, ... extensions and to only accept urls that start
     * with "https://www.ics.uci.edu/". In this case, we didn't need the
     * referringPage parameter to make the decision.
     */
    public MyCrawler() throws Exception{
        fetchFile = new CSVWriter(new FileWriter("res/fetch_usatoday.csv"));
        String [] fetchHead ={"URL","StatusCode"};
        fetchFile.writeNext(fetchHead);
        visitFile = new CSVWriter(new FileWriter("res/visit_usatoday.csv"));
        String [] visitHead = {"URL","Size","#ofOutlinks","Content-Type"};
        visitFile.writeNext(visitHead);
        urlsFile = new CSVWriter(new FileWriter("res/urls_usatoday.csv"));
        String [] urlsHead = {"URL","URL-Type"};
        urlsFile.writeNext(urlsHead);
        fetchCount=0;
    }
    @Override
    public void onBeforeExit(){
        super.onBeforeExit();
        System.out.println("WriteFiles(CSV)");
        try{
            fetchFile.close();
            visitFile.close();
            urlsFile.close();
        }catch(IOException e){
            e.printStackTrace();
        }
    }
    @Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        String url = webUrl.getURL().toLowerCase();
        String [] fetch_row= {url.replaceAll(",", "_"),""+statusCode};
        //System.out.println("fetch_row:"+fetch_row.toString());
        fetchFile.writeNext(fetch_row);
        fetchCount++;
        System.out.println("fetch count:"+fetchCount);
        visitedURLs.add(url);
    }
    @Override
    public boolean shouldVisit(Page referringPage, WebURL url) {
        String startUrl="usatoday.com"; //need to be the news site url
        String href = url.getURL().toLowerCase();
        boolean isReside = (href.startsWith("https://"+startUrl) || href.startsWith("http://"+startUrl) || href.startsWith("https://www."+startUrl) || href.startsWith("http://www."+startUrl) );
        /*
        String[] URLS_row;
        if(isReside){
            URLS_row = new String[]{href.replaceAll(",", "_"), "OK"};
        }else{
            URLS_row = new String[]{href.replaceAll(",", "_"), "N_OK"};
        }
        urlsFile.writeNext(URLS_row);
        */
        //System.out.println("URLS_rows:"+URLS_row);
        boolean hasNotVisited = !visitedURLs.contains(href);
        return !FILTERS.matcher(href).matches() && isReside && hasNotVisited; //seen or not seen need to be fixed
    }
    /**
     * This function is called when a page is fetched and ready
     * to be processed by your program.
     */
    @Override
    public void visit(Page page) {
        String url = page.getWebURL().getURL();
        System.out.println("URL: " + url);
        int numberOfOutLinks= 0;
        int contentSize = page.getContentData().length;
        String contentType = page.getContentType().split(";")[0];
        boolean isCorrectType = contentType.contains("html") || contentType.contains("doc") || contentType.contains("pdf") ||contentType.contains("image");
        if(isCorrectType){
            if (page.getParseData() instanceof HtmlParseData) {
                HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
                //String text = htmlParseData.getText();
                //String html = htmlParseData.getHtml();
                Set<WebURL> links = htmlParseData.getOutgoingUrls();
                //System.out.println("Text length: " + text.length());
                //System.out.println("Html length: " + html.length());
                //System.out.println("Number of outgoing links: " + links.size());
                //System.out.println(links);
                numberOfOutLinks=links.size();
                for(WebURL link:links){
                    String startUrl="usatoday.com";
                    String href = link.getURL().toLowerCase();;
                    boolean isReside = (href.startsWith("https://"+startUrl) || href.startsWith("http://"+startUrl) || href.startsWith("https://www."+startUrl) || href.startsWith("http://www."+startUrl) );
                    String[] URLS_row;
                    if(isReside){
                        URLS_row = new String[]{href.replaceAll(",", "_"), "OK"};
                    }else{
                        URLS_row = new String[]{href.replaceAll(",", "_"), "N_OK"};
                    }
                    urlsFile.writeNext(URLS_row);
                }
            }
            String [] visit_row={url.replaceAll(",", "_"),""+contentSize,""+numberOfOutLinks,contentType};
            visitFile.writeNext(visit_row);
            //System.out.println("visit_row:"+visit_row.toString());
        }
    }
}
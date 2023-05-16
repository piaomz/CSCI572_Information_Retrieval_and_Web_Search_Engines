import java.io.IOException;
import java.util.StringTokenizer;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class BigramIndex {
  public static class BigramMapper extends Mapper<Object, Text, Text, Text> {
    private final static Text docID = new Text();
    private Text word = new Text();
    private Text preword = new Text();
    private Text bigram = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String seperateTabText[] = value.toString().split("\t", 2);
      docID.set(seperateTabText[0]);
      StringTokenizer itr = new StringTokenizer(seperateTabText[1].toLowerCase().replaceAll("[^a-z]+", " "));
      if (itr.hasMoreTokens()) {
        preword.set(itr.nextToken());
      }
      while (itr.hasMoreTokens()) {
        word.set(itr.nextToken());
        bigram.set(preword.toString() + " " + word.toString());
        if(bigram.toString().equals("computer science") || bigram.toString().equals("information retrieval") || bigram.toString().equals("power politics")|| bigram.toString().equals("los angeles")|| bigram.toString().equals("bruce willis") ){
          context.write(bigram, docID);
        }
        preword.set(word.toString());
      }
    }
  }

  public static class BigramReducer extends Reducer<Text, Text, Text, Text> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context)
        throws IOException, InterruptedException {
      // int sum = 0;
      HashMap<String, Integer> counter = new HashMap<String, Integer>();
      for (Text val : values) {
        String docID = val.toString();
        if (counter.containsKey(docID)) {
          counter.put(docID, counter.get(docID) + 1);
        } else {
          counter.put(docID, 1);
        }
      }
      String formatOutput = "";
      for (Map.Entry<String, Integer> e : counter.entrySet()) {
        formatOutput = formatOutput + e.getKey() + ":" + e.getValue() + " ";
      }
      result.set(formatOutput);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "word count");

    job.setJarByClass(BigramIndex.class);
    job.setMapperClass(BigramMapper.class);
    // job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(BigramReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    FileInputFormat.addInputPath(job, new Path(args[0] + "/devdata"));
    FileOutputFormat.setOutputPath(job, new Path(args[1] + "/BigramOutput"));

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}// WordCount
